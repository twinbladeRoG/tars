import { Navigate, Outlet, useNavigate } from 'react-router';
import { Icon } from '@iconify/react';
import {
  ActionIcon,
  AppShell,
  Avatar,
  Burger,
  Card,
  Group,
  Menu,
  NavLink,
  ScrollArea,
  Skeleton,
  Text,
  Title,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { modals } from '@mantine/modals';
import { useQueryClient } from '@tanstack/react-query';

import { useActiveUser } from '@/apis/queries/auth.queries';
import { AnimatedThemeToggler } from '@/components/ui/animated-theme-toggler';

import AppNavLink from './AppNavLink';

const RootLayout = () => {
  const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
  const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(true);

  const user = useActiveUser();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const handleLogout = () => {
    modals.openConfirmModal({
      title: 'Are you sure you want to logout?',
      children: (
        <Text size="sm">
          This action will log you out of your account and you will need to log in again to access
          the application.
        </Text>
      ),
      labels: { confirm: 'Confirm', cancel: 'Cancel' },
      onCancel: () => {},
      onConfirm: async () => {
        localStorage.removeItem('ACCESS_TOKEN');
        localStorage.removeItem('REFRESH_TOKEN');
        queryClient.clear();
        await navigate('/');
      },
    });
  };

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 300,
        breakpoint: 'md',
        collapsed: { mobile: !mobileOpened, desktop: !desktopOpened },
      }}
      padding="md">
      <AppShell.Header>
        <Group h="100%" px="md">
          <Burger opened={mobileOpened} onClick={toggleMobile} hiddenFrom="md" size="md" />
          <Burger opened={desktopOpened} onClick={toggleDesktop} visibleFrom="md" size="md" />

          <Title order={3}>AI Resume Agent</Title>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <AppShell.Section grow component={ScrollArea}>
          <AppNavLink
            to="/agent"
            label="Chat"
            leftSection={<Icon icon="mingcute:ai-line" className="text-xl" />}
          />

          <NavLink
            href="#data-lab"
            label="Data Lab"
            leftSection={<Icon icon="hugeicons:ai-chemistry-03" className="text-xl" />}
            childrenOffset={28}
            defaultOpened>
            <AppNavLink
              to="/documents"
              label="Documents"
              leftSection={<Icon icon="mdi:file-document-multiple" className="text-xl" />}
            />
            <AppNavLink
              to="/knowledge-base"
              label="Knowledge Base"
              leftSection={<Icon icon="hugeicons:ai-book" className="text-xl" />}
            />
            <AppNavLink
              to="/candidates"
              label="Candidates"
              leftSection={<Icon icon="mdi:person-group" className="text-xl" />}
            />
          </NavLink>
        </AppShell.Section>

        <AppShell.Section>
          {user.isLoading ? (
            <Skeleton h={100} mt="sm" animate={false} />
          ) : (
            <Card>
              <div className="flex items-center gap-4">
                <Avatar size="md">
                  {user.data?.first_name?.charAt(0)}
                  {user.data?.last_name?.charAt(0)}
                </Avatar>
                <div className="">
                  <Text size="xs">
                    {user.data?.first_name} {user.data?.last_name}
                  </Text>
                  <Text size="xs">@{user.data?.username}</Text>
                </div>

                <AnimatedThemeToggler className="ml-auto" />

                <Menu>
                  <Menu.Target>
                    <ActionIcon variant="subtle">
                      <Icon icon="mdi:dots-vertical" className="text-2xl" />
                    </ActionIcon>
                  </Menu.Target>

                  <Menu.Dropdown>
                    <Menu.Item
                      leftSection={<Icon icon="mdi:logout" />}
                      color="red"
                      onClick={handleLogout}>
                      Logout
                    </Menu.Item>
                  </Menu.Dropdown>
                </Menu>
              </div>
            </Card>
          )}
        </AppShell.Section>
      </AppShell.Navbar>

      <AppShell.Main className="">
        {user.isError ? <Navigate to="/login" /> : <Outlet />}
      </AppShell.Main>
    </AppShell>
  );
};

export default RootLayout;
