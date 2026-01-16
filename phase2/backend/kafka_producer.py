"""
Kafka Producer for Phase 5 Event-Driven Architecture

This module handles publishing task events to Kafka topics.
Uses kafka-python library with proper error handling and logging.
"""

from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import os
from datetime import datetime
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092')
KAFKA_ENABLED = os.getenv('KAFKA_ENABLED', 'false').lower() == 'true'

# Initialize producer (lazy loading)
_producer = None

def get_producer() -> KafkaProducer:
    """Get or create Kafka producer instance"""
    global _producer
    
    if not KAFKA_ENABLED:
        logger.warning("Kafka is disabled. Set KAFKA_ENABLED=true to enable.")
        return None
    
    if _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKERS.split(','),
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                acks='all',  # Wait for all replicas
                retries=3,
                max_in_flight_requests_per_connection=1,
                compression_type='gzip'
            )
            logger.info(f"✅ Kafka producer connected to {KAFKA_BROKERS}")
        except KafkaError as e:
            logger.error(f"❌ Failed to create Kafka producer: {e}")
            _producer = None
    
    return _producer

def publish_event(topic: str, event_type: str, data: Dict[str, Any]) -> bool:
    """
    Publish an event to Kafka topic
    
    Args:
        topic: Kafka topic name (task-events, task.created, task.completed)
        event_type: Type of event (task.created, task.updated, task.completed, task.deleted)
        data: Event data (usually a task dict)
    
    Returns:
        bool: True if published successfully, False otherwise
    """
    producer = get_producer()
    
    if producer is None:
        logger.warning(f"Kafka disabled - Event not published: {event_type}")
        return False
    
    try:
        # Create event payload
        event = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        
        # Publish to topic
        future = producer.send(topic, value=event)
        
        # Wait for confirmation (optional, for reliability)
        record_metadata = future.get(timeout=10)
        
        logger.info(
            f"✅ Published {event_type} to {topic} "
            f"(partition={record_metadata.partition}, offset={record_metadata.offset})"
        )
        
        return True
        
    except KafkaError as e:
        logger.error(f"❌ Failed to publish {event_type} to {topic}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error publishing event: {e}")
        return False

def publish_task_created(task: Dict[str, Any]) -> bool:
    """Publish task.created event"""
    # Publish to both specific topic and general task-events topic
    success1 = publish_event('task.created', 'task.created', task)
    success2 = publish_event('task-events', 'task.created', task)
    return success1 or success2

def publish_task_updated(task: Dict[str, Any]) -> bool:
    """Publish task.updated event"""
    success1 = publish_event('task.updated', 'task.updated', task)
    success2 = publish_event('task-events', 'task.updated', task)
    return success1 or success2

def publish_task_completed(task: Dict[str, Any]) -> bool:
    """Publish task.completed event (triggers recurring task creation)"""
    success1 = publish_event('task.completed', 'task.completed', task)
    success2 = publish_event('task-events', 'task.completed', task)
    return success1 or success2

def publish_task_deleted(task_id: str, user_id: str) -> bool:
    """Publish task.deleted event"""
    data = {'task_id': task_id, 'user_id': user_id}
    success1 = publish_event('task.deleted', 'task.deleted', data)
    success2 = publish_event('task-events', 'task.deleted', data)
    return success1 or success2

def close_producer():
    """Close Kafka producer connection"""
    global _producer
    if _producer:
        _producer.flush()
        _producer.close()
        logger.info("Kafka producer closed")
        _producer = None
