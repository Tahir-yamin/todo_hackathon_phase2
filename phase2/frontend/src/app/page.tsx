'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from '@/lib/auth-client';

export default function Home() {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending) {
      if (session?.user) {
        // Authenticated user → redirect to dashboard
        router.push('/dashboard');
      } else {
        // Unauthenticated user → redirect to landing
        router.push('/landing');
      }
    }
  }, [session, isPending, router]);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <p className="text-white">Loading...</p>
    </div>
  );
}