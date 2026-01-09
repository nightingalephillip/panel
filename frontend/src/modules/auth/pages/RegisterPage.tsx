import { AuthLayout } from '@/layouts';
import { RegisterForm } from '../components/RegisterForm';

export function RegisterPage() {
  return (
    <AuthLayout
      title="Create your account"
      subtitle="OSINT Investigation Dashboard"
    >
      <RegisterForm />
    </AuthLayout>
  );
}
