'use client';

import { useState, useEffect } from 'react';
import { 
  signInWithPopup, 
  signOut, 
  User,
  onAuthStateChanged 
} from 'firebase/auth';
import { auth, googleProvider } from '@/lib/firebase';

interface AuthState {
  user: User | null;
  loading: boolean;
  token: string | null;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    loading: true,
    token: null,
  });

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        try {
          const token = await user.getIdToken();
          setAuthState({ user, loading: false, token });
        } catch (error) {
          console.error('Error getting token:', error);
          setAuthState({ user, loading: false, token: null });
        }
      } else {
        setAuthState({ user: null, loading: false, token: null });
      }
    });

    return () => unsubscribe();
  }, []);

  const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      return result.user;
    } catch (error: any) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  };

  return {
    ...authState,
    signInWithGoogle,
    logout,
  };
}

