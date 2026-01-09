import { AuthLayout } from '@/layouts';
import { LoginForm } from '../components/LoginForm';

export function LoginPage() {
  return (
    <AuthLayout
      title="Sign in to your account"
      subtitle="OSINT Investigation Dashboard"
    >
      <LoginForm />
    </AuthLayout>
  );
}
