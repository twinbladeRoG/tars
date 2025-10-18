import { createBrowserRouter } from 'react-router';
import { RouterProvider } from 'react-router/dom';

import Home from './pages';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
]);

const Router = () => <RouterProvider router={router} />;

export default Router;
