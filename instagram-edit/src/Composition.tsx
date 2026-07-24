import React from "react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Composition,
  Easing,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Video } from "@remotion/media";
import { getVideoDuration } from "./get-video-duration";
import "./fonts.css";

const GOLD = "#c49a2a";
const CREAM = "#e8e0d0";
const DARK = "#0a0a0a";

type Props = { videoSrc: string };

const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const duration = await getVideoDuration(props.videoSrc);
  return {
    durationInFrames: Math.ceil(duration * 30),
    width: 1080,
    height: 1920,
    fps: 30,
  };
};

// ─── Cinematic bars ───────────────────────────────────────────────────────────
const CinematicBars: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const BAR = 90;

  const progress = interpolate(
    frame,
    [0, 22, durationInFrames - 18, durationInFrames],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.bezier(0.16, 1, 0.3, 1),
    }
  );

  const topY = interpolate(progress, [0, 1], [-BAR, 0]);
  const botY = interpolate(progress, [0, 1], [BAR, 0]);

  return (
    <>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: BAR,
          background: DARK,
          translate: `0 ${topY}px`,
          zIndex: 10,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: BAR,
          background: DARK,
          translate: `0 ${botY}px`,
          zIndex: 10,
        }}
      />
    </>
  );
};

// ─── Fade overlay ─────────────────────────────────────────────────────────────
const FadeOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const opacity = interpolate(
    frame,
    [0, 20, durationInFrames - 20, durationInFrames],
    [1, 0, 0, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        background: DARK,
        opacity,
        zIndex: 20,
        pointerEvents: "none",
      }}
    />
  );
};

// ─── Progress bar ─────────────────────────────────────────────────────────────
const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const appear = interpolate(frame, [20, 40], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const progress = frame / durationInFrames;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height: 5,
        background: "rgba(255,255,255,0.1)",
        zIndex: 30,
        opacity: appear,
      }}
    >
      <div
        style={{
          height: "100%",
          background: `linear-gradient(90deg, ${GOLD}, #e8c55a)`,
          width: `${progress * 100}%`,
          boxShadow: `0 0 14px ${GOLD}`,
        }}
      />
    </div>
  );
};

// ─── Brand watermark ─────────────────────────────────────────────────────────
const BrandMark: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames: dur } = useVideoConfig();

  const inProgress = interpolate(frame, [0, 35], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const outProgress = interpolate(frame, [dur - 30, dur], [0, 1], {
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.7, 0, 0.84, 0),
  });

  const opacity = inProgress * (1 - outProgress);
  const slideY = interpolate(inProgress, [0, 1], [30, 0]);
  const lineW = interpolate(inProgress, [0, 1], [0, 180]);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 130,
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 8,
        opacity,
        translate: `0 ${slideY}px`,
        zIndex: 15,
      }}
    >
      <div
        style={{
          width: lineW,
          height: 1,
          background: `linear-gradient(90deg, transparent, ${GOLD}, transparent)`,
        }}
      />
      <div
        style={{
          fontFamily: "'Frank Ruhl Libre', serif",
          fontSize: 58,
          fontWeight: 900,
          color: CREAM,
          letterSpacing: "0.04em",
          textShadow: `0 4px 32px rgba(0,0,0,0.8)`,
          direction: "rtl",
          lineHeight: 1,
        }}
      >
        אילן לוי
      </div>
      <div
        style={{
          fontFamily: "'Assistant', sans-serif",
          fontSize: 22,
          fontWeight: 400,
          color: GOLD,
          letterSpacing: "0.25em",
          textTransform: "uppercase",
          textShadow: `0 2px 16px rgba(0,0,0,0.6)`,
        }}
      >
        ליווי אישי · רמת השרון
      </div>
      <div
        style={{
          width: lineW * 0.65,
          height: 1,
          background: `linear-gradient(90deg, transparent, ${GOLD}, transparent)`,
        }}
      />
    </div>
  );
};

// ─── Animated grain overlay ───────────────────────────────────────────────────
const GrainOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const seed = Math.floor(frame / 2);

  return (
    <AbsoluteFill
      style={{
        opacity: 0.055,
        mixBlendMode: "overlay",
        zIndex: 5,
        pointerEvents: "none",
      }}
    >
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0 }}>
        <filter id={`g${seed}`}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.68"
            numOctaves="4"
            seed={seed}
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

// ─── Vignette overlay ─────────────────────────────────────────────────────────
const VignetteOverlay: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse 80% 90% at 50% 50%, transparent 35%, rgba(0,0,0,0.7) 100%)",
      zIndex: 4,
      pointerEvents: "none",
    }}
  />
);

// ─── Colour-graded video with Ken Burns ──────────────────────────────────────
const VideoLayer: React.FC<{ src: string }> = ({ src }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.065], {
    extrapolateRight: "clamp",
  });

  const sepia = interpolate(frame, [0, 60], [0.2, 0.05], { extrapolateRight: "clamp" });
  const bright = interpolate(frame, [0, 40], [0.85, 1.0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: DARK }}>
      <Video
        src={src}
        objectFit="cover"
        style={{
          width: "100%",
          height: "100%",
          scale: String(scale),
          filter: `sepia(${sepia}) saturate(1.3) contrast(1.1) brightness(${bright})`,
        }}
        volume={(f) =>
          interpolate(
            f,
            [0, 22, durationInFrames - 22, durationInFrames],
            [0, 1, 1, 0],
            { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
          )
        }
      />
    </AbsoluteFill>
  );
};

// ─── Main composition ─────────────────────────────────────────────────────────
const InstagramEdit: React.FC<Props> = ({ videoSrc }) => {
  const { durationInFrames } = useVideoConfig();
  const brandStart = 45;
  const brandDur = Math.min(durationInFrames - brandStart - 40, 150);

  return (
    <AbsoluteFill style={{ background: DARK, overflow: "hidden" }}>
      <Sequence name="Video">
        <VideoLayer src={videoSrc} />
      </Sequence>

      <Sequence name="Grain">
        <GrainOverlay />
      </Sequence>

      <Sequence name="Vignette">
        <VignetteOverlay />
      </Sequence>

      <Sequence name="CinematicBars">
        <CinematicBars />
      </Sequence>

      {brandDur > 0 && (
        <Sequence name="BrandMark" from={brandStart} durationInFrames={brandDur}>
          <BrandMark />
        </Sequence>
      )}

      <Sequence name="ProgressBar">
        <ProgressBar />
      </Sequence>

      <Sequence name="Fade">
        <FadeOverlay />
      </Sequence>
    </AbsoluteFill>
  );
};

// ─── Composition registration ─────────────────────────────────────────────────
export const MyComposition: React.FC = () => {
  const videoSrc = staticFile("source.mp4");
  return (
    <Composition
      id="InstagramEdit"
      component={InstagramEdit}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{ videoSrc }}
      calculateMetadata={calculateMetadata}
    />
  );
};

export const MyComponent = InstagramEdit;
