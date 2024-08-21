// components/forms/user-auth-form.tsx
'use client';

import { Button } from '@/components/ui/button';
import { useState } from 'react';
import UserRegisterForm from "./user-register-form"
import UserLoginForm from "./user-login-form"
import GithubSignInButton from '../github-auth-button';

interface UserAuthFormProps {
  onFormChange: (showRegisterForm: boolean) => void;
}

export default function UserAuthForm({ onFormChange }: UserAuthFormProps) {
  const [showRegisterForm, setShowRegisterForm] = useState(false); // State to handle form switch
  const [loading, setLoading] = useState(false); // Handle loading state

  const handleRegisterClick = () => {
    setShowRegisterForm(true); // Show registration form
    onFormChange(true); // Notify parent to show registration form
  };

  const handleLoginClick = () => {
    setShowRegisterForm(false); // Hide registration form
    onFormChange(false); // Notify parent to show login form
  };

  return (
    <div className="flex flex-col space-y-4">
      {showRegisterForm ? (
        <>
          <UserRegisterForm /> {/* Show registration form if needed */}
          <Button
            className="hover:bg-beige mt-4 w-full border border-black bg-white text-black"
            onClick={handleLoginClick}
            disabled={loading}
          >
            Back to Login
          </Button>
        </>
      ) : (
        <>
          <UserLoginForm /> {/* Show login form if needed */}
          <Button
            className="hover:bg-beige mt-4 w-full border border-black bg-white text-black"
            onClick={handleRegisterClick}
            disabled={loading}
          >
            Register
          </Button>
        </>
      )}
      <div className="relative mt-4">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Or continue with
          </span>
        </div>
      </div>
      <GithubSignInButton />
    </div>
  );
}
