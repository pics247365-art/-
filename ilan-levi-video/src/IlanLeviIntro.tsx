import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  useCurrentFrame,
  Interactive,
  random,
} from "remotion";
import { loadFonts, FRANK_RUHL, ASSISTANT, PLAYFAIR } from "./fonts";

loadFonts();

const BG = "#0a0a0a";
const CREAM = "#e8e0d0";
const GOLD = "#c49a2a";
const RED = "#a81818";
const WARM = "#c8a97a";

// ── Vignette overlay ──────────────────────────────────────────
const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,0.7) 80%, rgba(0,0,0,0.95) 100%)",
      pointerEvents: "none",
      zIndex: 15,
    }}
  />
);

// ── Scanlines overlay ─────────────────────────────────────────
const Scanlines: React.FC = () => (
  <AbsoluteFill
    style={{
      backgroundImage:
        "repeating-linear-gradient(0deg, rgba(0,0,0,0.06) 0px, rgba(0,0,0,0.06) 1px, transparent 1px, transparent 4px)",
      pointerEvents: "none",
      zIndex: 14,
    }}
  />
);

// ── Grain overlay ─────────────────────────────────────────────
const Grain: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", opacity: 0.2, zIndex: 13 }}>
    <svg width="100%" height="100%">
      <filter id="grain3">
        <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="4" stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#grain3)" />
    </svg>
  </AbsoluteFill>
);

// ── Chromatic aberration on text via layered shadows ───────────
const GlitchName: React.FC<{ aberration: number; opacity: number; scale: number }> = ({
  aberration,
  opacity,
  scale,
}) => {
  const ab = aberration;
  return (
    <div style={{ position: "relative", opacity, scale: String(scale), textAlign: "center" }}>
      {/* Red channel — offset right */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          fontFamily: `${FRANK_RUHL}, serif`,
          fontSize: 148,
          fontWeight: 900,
          color: "transparent",
          textShadow: `${ab}px 0 0 rgba(200,30,30,0.7)`,
          textAlign: "center",
          userSelect: "none",
        }}
      >
        אילן לוי
      </div>
      {/* Cyan channel — offset left */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          fontFamily: `${FRANK_RUHL}, serif`,
          fontSize: 148,
          fontWeight: 900,
          color: "transparent",
          textShadow: `${-ab / 2}px 0 0 rgba(30,200,200,0.45)`,
          textAlign: "center",
          userSelect: "none",
        }}
      >
        אילן לוי
      </div>
      {/* Main gold text */}
      <div
        style={{
          position: "relative",
          fontFamily: `${FRANK_RUHL}, serif`,
          fontSize: 148,
          fontWeight: 900,
          color: GOLD,
          letterSpacing: "0.02em",
          lineHeight: 1,
          textAlign: "center",
          textShadow:
            ab > 1
              ? `0 0 ${ab * 3}px rgba(196,154,42,0.35)`
              : undefined,
        }}
      >
        אילן לוי
      </div>
    </div>
  );
};

// ── Light sweep: moves right → left ──────────────────────────
const LightSweep: React.FC<{ frame: number }> = ({ frame }) => {
  // First sweep: frames 60–130
  const x1 = interpolate(frame, [60, 130], [120, -30], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.4, 0, 0.6, 1),
  });
  const op1 = interpolate(frame, [60, 72, 118, 130], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Second sweep: frames 200–255
  const x2 = interpolate(frame, [200, 255], [120, -30], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.4, 0, 0.6, 1),
  });
  const op2 = interpolate(frame, [200, 210, 248, 255], [0, 0.7, 0.7, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const sweepStyle = (xPercent: number, opacity: number): React.CSSProperties => ({
    position: "absolute",
    inset: 0,
    opacity,
    background: `linear-gradient(
      105deg,
      transparent ${xPercent - 12}%,
      rgba(255,240,180,0.07) ${xPercent - 4}%,
      rgba(255,240,180,0.22) ${xPercent}%,
      rgba(255,240,180,0.07) ${xPercent + 4}%,
      transparent ${xPercent + 12}%
    )`,
    pointerEvents: "none",
    zIndex: 16,
  });

  return (
    <>
      {op1 > 0 && <div style={sweepStyle(x1, op1)} />}
      {op2 > 0 && <div style={sweepStyle(x2, op2)} />}
    </>
  );
};

// ── Random glitch bar ─────────────────────────────────────────
const GlitchBars: React.FC<{ frame: number }> = ({ frame }) => {
  if (random(`bars-${frame}`) >= 0.1) return null;
  const y1 = Math.floor(random(`y1-${frame}`) * 1920);
  const y2 = Math.floor(random(`y2-${frame}`) * 1920);
  const w1 = `${15 + random(`w1-${frame}`) * 45}%`;
  const w2 = `${8 + random(`w2-${frame}`) * 25}%`;
  const color = random(`col-${frame}`) > 0.5 ? GOLD : RED;
  return (
    <>
      <div style={{ position: "absolute", top: y1, left: 0, width: w1, height: 1, background: color, opacity: 0.55, zIndex: 9 }} />
      <div style={{ position: "absolute", top: y2, right: 0, width: w2, height: 1, background: GOLD, opacity: 0.35, zIndex: 9 }} />
    </>
  );
};

// ── Divider line ──────────────────────────────────────────────
const DividerLine: React.FC = () => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [0, 35], ["0%", "55%"], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return <div style={{ width, height: 1, background: GOLD, margin: "0 auto" }} />;
};

// ── Service item with varying size ────────────────────────────
const ServiceItem: React.FC<{ text: string; size: number; color: string }> = ({
  text,
  size,
  color,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 22], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const tx = interpolate(frame, [0, 22], [-24, 0], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return (
    <Interactive.Div
      name={`Service: ${text}`}
      style={{
        opacity,
        translate: `${tx}px 0px`,
        fontFamily: `${ASSISTANT}, sans-serif`,
        fontSize: size,
        fontWeight: size > 44 ? 400 : 300,
        color,
        letterSpacing: size > 44 ? "0.04em" : "0.1em",
        direction: "rtl",
        lineHeight: 1.25,
        textAlign: "center",
      }}
    >
      {text}
    </Interactive.Div>
  );
};

// ─────────────────────────────────────────────────────────────
export const IlanLeviIntro: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  // Name
  const nameOpacity = interpolate(frame, [18, 60], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const nameScale = interpolate(frame, [18, 65], [1.1, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Chromatic aberration: big on entry → settles → random spikes
  const baseAb = interpolate(frame, [18, 75], [16, 0.2], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const spike = random(`sp-${frame}`) < 0.05 ? random(`amt-${frame}`) * 10 : 0;
  const aberration = baseAb + spike;

  // Tagline
  const tagOpacity = interpolate(frame, [75, 108], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Label
  const labelOpacity = interpolate(frame, [40, 75], [0, 1], { extrapolateRight: "clamp" });

  // Accent bar
  const accentH = interpolate(frame, [12, 68], ["0%", "26%"], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Contact
  const contactOpacity = interpolate(frame, [238, 272], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const services = [
    { text: "ביקור בבית", size: 54, color: CREAM },
    { text: "שיחה וקפה", size: 36, color: WARM },
    { text: "טיול ביחד", size: 48, color: CREAM },
    { text: "משחק שחמט", size: 32, color: WARM },
  ];

  return (
    <AbsoluteFill style={{ background: BG, opacity: bgOpacity }}>
      <Grain />
      <Scanlines />
      <Vignette />
      <LightSweep frame={frame} />
      <GlitchBars frame={frame} />

      {/* Gold accent vertical bar */}
      <div
        style={{
          position: "absolute",
          right: 52,
          top: "28%",
          width: 2,
          height: accentH,
          background: GOLD,
          transform: "translateY(-50%)",
          zIndex: 8,
        }}
      />

      {/* Small label — top left */}
      <div
        style={{
          position: "absolute",
          top: 80,
          left: 60,
          opacity: labelOpacity,
          zIndex: 8,
          fontFamily: `${ASSISTANT}, sans-serif`,
          fontSize: 20,
          color: GOLD,
          letterSpacing: "0.22em",
          direction: "ltr",
          textTransform: "uppercase",
        }}
      >
        personal accompaniment
      </div>

      {/* Index — top right */}
      <div
        style={{
          position: "absolute",
          top: 80,
          right: 60,
          opacity: labelOpacity * 0.35,
          zIndex: 8,
          fontFamily: `${FRANK_RUHL}, serif`,
          fontWeight: 900,
          fontSize: 22,
          color: CREAM,
          letterSpacing: "0.15em",
          direction: "ltr",
        }}
      >
        01
      </div>

      {/* ── MAIN CONTENT ── */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "0 72px",
          direction: "rtl",
          zIndex: 8,
        }}
      >
        {/* NAME with chromatic aberration */}
        <GlitchName aberration={aberration} opacity={nameOpacity} scale={nameScale} />

        {/* Divider */}
        <div style={{ marginTop: 30, marginBottom: 28, width: "100%" }}>
          <Sequence name="Divider" from={78} layout="none">
            <DividerLine />
          </Sequence>
        </div>

        {/* TAGLINE */}
        <Interactive.Div
          name="Tagline"
          style={{
            opacity: tagOpacity,
            fontFamily: `${PLAYFAIR}, serif`,
            fontStyle: "italic",
            fontSize: 50,
            color: WARM,
            letterSpacing: "0.05em",
            textAlign: "center",
            lineHeight: 1.3,
            marginBottom: 68,
          }}
        >
          ליווי אישי · קשר אנושי
        </Interactive.Div>

        {/* SERVICES — varying sizes, centered */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 12,
            width: "100%",
          }}
        >
          {services.map((s, i) => (
            <Sequence key={s.text} name={`Service ${i + 1}`} from={128 + i * 20} layout="none">
              <ServiceItem text={s.text} size={s.size} color={s.color} />
            </Sequence>
          ))}
        </div>

        {/* PHONE — glowing gold */}
        <Interactive.Div
          name="Phone"
          style={{
            opacity: contactOpacity,
            marginTop: 80,
            fontFamily: `${FRANK_RUHL}, serif`,
            fontWeight: 900,
            fontSize: 56,
            color: GOLD,
            letterSpacing: "0.06em",
            textAlign: "center",
            direction: "ltr",
            textShadow: `0 0 ${24 * contactOpacity}px rgba(196,154,42,0.6), 0 0 ${8 * contactOpacity}px rgba(196,154,42,0.8)`,
          }}
        >
          052-864-6446
        </Interactive.Div>

        <Interactive.Div
          name="Location"
          style={{
            opacity: contactOpacity * 0.75,
            marginTop: 16,
            fontFamily: `${ASSISTANT}, sans-serif`,
            fontWeight: 300,
            fontSize: 28,
            color: CREAM,
            letterSpacing: "0.14em",
            textAlign: "center",
          }}
        >
          רמת השרון והסביבה
        </Interactive.Div>
      </AbsoluteFill>

      {/* Bottom gradient line */}
      <div
        style={{
          position: "absolute",
          bottom: 88,
          left: "18%",
          right: "18%",
          height: 1,
          background: `linear-gradient(to right, transparent, ${GOLD}, transparent)`,
          opacity: contactOpacity * 0.4,
          zIndex: 8,
        }}
      />
    </AbsoluteFill>
  );
};
