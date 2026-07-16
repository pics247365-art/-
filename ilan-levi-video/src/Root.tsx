import "./index.css";
import { Composition } from "remotion";
import { IlanLeviIntro } from "./IlanLeviIntro";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="IlanLeviIntro"
        component={IlanLeviIntro}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
