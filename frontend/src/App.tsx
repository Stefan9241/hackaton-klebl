import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import TableChartIcon from '@mui/icons-material/TableChart';
import { AppProvider } from '@toolpad/core/react-router-dom';
import { Outlet } from 'react-router-dom';
import type { Navigation } from '@toolpad/core';

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Navigation',
  },
  {
    title: 'Import PDF Drawing',
    icon: <PictureAsPdfIcon />,
  },
  {
    segment: 'Drawings',
    title: 'Drawings',
    icon: <TableChartIcon />,
  },
];

const BRANDING = {
  title: 'Klebl Data Extractor',
};

export default function App() {
  return (
    <AppProvider navigation={NAVIGATION} branding={BRANDING}>
      <Outlet />
    </AppProvider>
  );
}
