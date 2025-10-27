import { Link, useLocation } from 'react-router';
import { NavLink, type NavLinkProps } from '@mantine/core';

interface AppNavLinkProps extends NavLinkProps {
  to: string;
}

const AppNavLink: React.FC<AppNavLinkProps> = ({ to, ...props }) => {
  const location = useLocation();

  return <NavLink component={Link} to={to} {...props} active={location.pathname === to} />;
};

export default AppNavLink;
