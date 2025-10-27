import LoginForm from '@/components/modules/auth/LoginForm';

const LoginPage = () => {
  return (
    <main className="flex min-h-dvh flex-col justify-center bg-white p-8">
      <LoginForm className="bg-primary mx-auto w-full max-w-3xl rounded-xl p-8 shadow-2xl" />
    </main>
  );
};

export default LoginPage;
