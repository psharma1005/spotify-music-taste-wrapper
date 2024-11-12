import * as React from 'react';
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import ColorModeSelect from '../shared-theme/ColorModeSelect';
import AppTheme from '../shared-theme/AppTheme';
import CssBaseline from '@mui/material/CssBaseline';

const PageContainer = styled(Stack)(({ theme }) => ({
    height: 'calc((1 - var(--template-frame-height, 0)) * 100dvh)',
    minHeight: '100%',
    padding: theme.spacing(2),
    [theme.breakpoints.up('sm')]: {
      padding: theme.spacing(4),
    },
    '&::before': {
      content: '""',
      display: 'block',
      position: 'absolute',
      zIndex: -1,
      inset: 0,
      backgroundImage:
        'radial-gradient(ellipse at 50% 50%, hsl(210, 100%, 97%), hsl(0, 0%, 100%))',
      backgroundRepeat: 'no-repeat',
      ...theme.applyStyles('dark', {
        backgroundImage:
          'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
      }),
    },
  }));

export default function MainPage(props) {
    return (
        <AppTheme {...props}>
            <CssBaseline enableColorScheme />
            <PageContainer direction="column" justifyContent="space-between" sx={{ fontFamily: 'Arial, sans-serif' }}>
                <ColorModeSelect sx={{ position: 'fixed', top: '1rem', right: '1rem', fontFamily: 'Arial, sans-serif' }} />
                <div>
                    <h1>Spotify Wrapper</h1>
                    <p>Spotify Wrapper is a web application that allows users to search for songs, albums, and artists on Spotify. Users can also view their top tracks and top artists on Spotify.</p>
                    <p>To get started, click the "Link Spotify" button below to link your Spotify account.</p>
                    <p>Once your Spotify account is linked, you can search for songs, albums, and artists on Spotify using the search bar at the top of the page.</p>
                    <p>You can also view your top tracks and top artists on Spotify by clicking the "Top Tracks" and "Top Artists" buttons below.</p>
                    <p>Enjoy using Spotify Wrapper!</p>
                </div>
                </PageContainer>
        </AppTheme>
    );
}