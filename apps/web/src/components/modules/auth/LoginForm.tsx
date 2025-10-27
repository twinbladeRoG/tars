import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router';
import { yupResolver } from '@hookform/resolvers/yup';
import { Button, PasswordInput, TextInput } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import * as yup from 'yup';

import { useLogin } from '@/apis/queries/auth.queries';

const schema = yup.object({
  username: yup.string().required(),
  password: yup.string().required(),
});

interface LoginFormProps {
  className?: string;
}

const LoginForm: React.FC<LoginFormProps> = ({ className }) => {
  const form = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      username: '',
      password: '',
    },
  });

  const login = useLogin();
  const navigate = useNavigate();

  const handleSubmit = form.handleSubmit((data) => {
    login.mutate(data, {
      onSuccess: async (res) => {
        localStorage.setItem('ACCESS_TOKEN', res.tokens.access_token);
        localStorage.setItem('REFRESH_TOKEN', res.tokens.refresh_token);

        await navigate('/agent');
      },
      onError: (error) => {
        notifications.show({
          title: 'Oops! Something went wrong',
          message: error.message,
          color: 'red',
        });
      },
    });
  });

  return (
    <form className={className} onSubmit={handleSubmit}>
      <h1 className="mb-3 text-center text-2xl font-bold">Login</h1>

      <TextInput
        {...form.register('username')}
        error={form.formState.errors.username?.message}
        type="email"
        label="Email"
        placeholder="Email"
        mb="lg"
      />
      <PasswordInput
        {...form.register('password')}
        error={form.formState.errors.password?.message}
        label="Password"
        placeholder="Password"
        mb="lg"
      />

      <Button fullWidth type="submit" loading={login.isPending}>
        Login
      </Button>
    </form>
  );
};

export default LoginForm;
