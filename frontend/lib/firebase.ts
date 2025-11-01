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
  apiKey: "AIzaSyCyfnt8HefiXgnNaY4T1bMA_hOmb032Qkg",
  authDomain: "lexsy-d1627.firebaseapp.com",
  projectId: "lexsy-d1627",
  storageBucket: "lexsy-d1627.firebasestorage.app",
  messagingSenderId: "817150269429",
  appId: "1:817150269429:web:f6802d8d919812a10132bc",
  measurementId: "G-BV50JWYMPG"
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

