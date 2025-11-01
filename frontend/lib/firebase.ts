/**
 * Firebase Configuration and Setup
 * 
 * Instructions:
 * 1. Go to Firebase Console: https://console.firebase.google.com/
 * 2. Create a project or select existing
 * 3. Enable Google Authentication in Authentication section
 * 4. Get Web App config from Project Settings → Your apps
 * 5. Replace the values below with your Firebase config
 */

import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

// Firebase configuration for Lexsy
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyATjXWNHuFB6L_OaXZRjMf41ZgVeo7q524",
  authDomain: "lexsy-ai-app.firebaseapp.com",
  projectId: "lexsy-ai-app",
  storageBucket: "lexsy-ai-app.firebasestorage.app",
  messagingSenderId: "885588494049",
  appId: "1:885588494049:web:87bd8e80741930cd0cd9a0",
  measurementId: "G-JXCZ7BPX0C"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Auth
export const auth = getAuth(app);

// Configure Google Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account' // Always show account picker
});

export default app;

