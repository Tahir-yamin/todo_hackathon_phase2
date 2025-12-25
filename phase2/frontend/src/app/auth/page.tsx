'use client';

import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2, Mail, Lock, User, Github, ArrowRight, CheckCircle2, AlertCircle } from "lucide-react";

export default function AuthPage() {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSocialSignIn = async (provider: "google" | "github") => {
    try {
      await authClient.signIn.social({
        provider: provider,
        callbackURL: "/dashboard",
      });
    } catch (err: any) {
      setError(err.message || `${provider} sign-in failed`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isLoginMode) {
        // --- LOGIN FLOW ---
        const { data, error } = await authClient.signIn.email({
          email,
          password,
        });

        if (error) throw error;
        router.push("/dashboard");
      } else {
        // --- SIGN UP FLOW ---
        const { data, error } = await authClient.signUp.email({
          email,
          password,
          name,
        });

        if (error) throw error;

        // ✅ SECURITY: Verification Alert
        alert("Account created! 📧 Please check your email (or terminal) to verify your account before logging in.");
        setIsLoginMode(true); // Switch back to login
        setEmail('');
        setPassword('');
        setName('');
      }
    } catch (err: any) {
      setError(err.message || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Blobs */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[120px]" />
      </div>

      <div className="w-full max-w-md bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl relative z-10">
        <div className="text-center mb-8">
        </AnimatePresence>

        {!isLoginMode && (
          <div className="space-y-1">
            <label className="text-sm font-medium text-slate-300 ml-1">Name</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
              <input
                type="text"
                required
                placeholder="John Doe"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-10 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          </div>
        )}

        <div className="space-y-1">
          <label className="text-sm font-medium text-slate-300 ml-1">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
            <input
              type="email"
              required
              placeholder="you@example.com"
              className="w-full bg-white/5 border border-white/10 rounded-xl px-10 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium text-slate-300 ml-1">Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
            <input
              type="password"
              required
              placeholder="••••••••"
              className="w-full bg-white/5 border border-white/10 rounded-xl px-10 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-medium py-3 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Processing...
            </>
'use client';

          import {useState} from "react";
          import {authClient} from "@/lib/auth-client";
          import {useRouter} from "next/navigation";
          import {motion, AnimatePresence} from "framer-motion";
          import {Loader2, Mail, Lock, User, Github, ArrowRight, CheckCircle2, AlertCircle} from "lucide-react";

          export default function AuthPage() {
  const [isLoginMode, setIsLoginMode] = useState(true);
          const [email, setEmail] = useState("");
          const [password, setPassword] = useState("");
          const [name, setName] = useState("");
          const [loading, setLoading] = useState(false);
          const [error, setError] = useState<string | null>(null);
          const router = useRouter();

  const handleSocialSignIn = async (provider: "google" | "github") => {
    try {
            await authClient.signIn.social({
              provider: provider,
              callbackURL: "/dashboard",
            });
    } catch (err: any) {
            setError(err.message || `${provider} sign-in failed`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
            e.preventDefault();
          setLoading(true);
          setError(null);

          try {
      if (isLoginMode) {
        // --- LOGIN FLOW ---
        const {data, error} = await authClient.signIn.email({
            email,
            password,
        });

          if (error) throw error;
          router.push("/dashboard");
      } else {
        // --- SIGN UP FLOW ---
        const {data, error} = await authClient.signUp.email({
            email,
            password,
            name,
        });

          if (error) throw error;

          // ✅ SECURITY: Verification Alert
          alert("Account created! 📧 Please check your email (or terminal) to verify your account before logging in.");
          setIsLoginMode(true); // Switch back to login
          setEmail('');
          setPassword('');
          setName('');
      }
    } catch (err: any) {
            setError(err.message || "Authentication failed");
    } finally {
            setLoading(false);
    }
  };

          return (
          <div className="min-h-screen bg-[#020617] flex items-center justify-center p-4 relative overflow-hidden">
            {/* Background Blobs */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
              <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-[120px]" />
              <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[120px]" />
            </div>

            <div className="w-full max-w-md bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl relative z-10">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">
                  {isLoginMode ? "Welcome Back!" : "Join Us!"}
                </h1>
                <p className="text-slate-400">
                  {isLoginMode ? "Sign in to your account" : "Create your new account"}
                </p>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-xl mb-6 flex items-center gap-3"
                >
                  <AlertCircle className="w-5 h-5" />
                  <span className="text-sm">{error}</span>
                </motion.div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                <AnimatePresence mode="wait">
                  {!isLoginMode && (
                    <motion.div
                      key="nameField"
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.2 }}
                      className="overflow-hidden"
                    >
                      <div className="space-y-1">
                        <label className="text-sm font-medium text-slate-300 ml-1">Name</label>
                        <div className="relative">
                          <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                          <input
                            type="text"
                            required
                            placeholder="John Doe"
                            className="w-full bg-white/5 border border-white/10 rounded-xl px-10 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                          />
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-300 ml-1">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                    <input
                      type="email"
                      required
                      placeholder="you@example.com"
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-10 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-300 ml-1">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                    <input
                      type="password"
                      required
                      placeholder="••••••••"
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-10 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-medium py-3 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      {isLoginMode ? "Sign In" : "Create Account"}
                      <ArrowRight className="w-5 h-5" />
                    </>
                  )}
                </button>
              </form>

              {/* Social Login - GitHub Only (Google disabled due to Vercel domain restrictions) */}
              <div className="mb-6 mt-6"> {/* Added mt-6 for spacing */}
                <button
                  onClick={() => handleSocialSignIn("github")}
                  className="w-full flex items-center justify-center gap-2 bg-[#24292F] hover:bg-[#1c2127] text-white border border-white/10 rounded-xl py-3 transition-all font-medium"
                >
                  <Github className="w-5 h-5 text-white" />
                  <span className="text-white font-medium">Continue with GitHub</span>
                </button>
              </div>

              <div className="mt-6 text-center">
                <button
                  onClick={() => {
                    setIsLoginMode(!isLoginMode);
                    setError(null);
                  }}
                  className="text-purple-400 hover:text-purple-300 text-sm transition-colors"
                >
                  {isLoginMode ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
                </button>
              </div>
            </div>
          </div >
          );
}