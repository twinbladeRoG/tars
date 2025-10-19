import { useNavigate } from 'react-router';

import { RainbowButton } from '@/components/ui/rainbow-button';
import { RetroGrid } from '@/components/ui/retro-grid';
import { SmoothCursor } from '@/components/ui/smooth-cursor';

const Home = () => {
  const navigate = useNavigate();
  const handleChat = async () => {
    await navigate('/agent');
  };

  return (
    <main>
      <section className="relative h-dvh w-full bg-white">
        <div className="absolute top-1/2 left-1/2 flex -translate-1/2 flex-col items-center">
          <h1 className="mb-6 text-center">
            <span className="pointer-events-none z-10 bg-gradient-to-b from-[#ffd319] via-[#ff2975] to-[#8c1eff] bg-clip-text text-center text-7xl leading-none font-bold tracking-tighter whitespace-pre-wrap text-transparent">
              AI Resume Agent
            </span>
          </h1>

          <RainbowButton onClick={handleChat}>Chat</RainbowButton>
        </div>
        <RetroGrid />
      </section>
      <SmoothCursor />
    </main>
  );
};

export default Home;
