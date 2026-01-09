import { ReactNode } from 'react';

interface AuthLayoutProps {
  children: ReactNode;
  title: string;
  subtitle?: string;
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white">{title}</h1>
          {subtitle && (
            <p className="mt-2 text-gray-400">{subtitle}</p>
          )}
        </div>
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          {children}
        </div>
      </div>
    </div>
  );
}
