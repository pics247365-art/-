import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  useCurrentFrame,
  Interactive,
} from "remotion";
import { loadFonts, FRANK_RUHL, ASSISTANT, PLAYFAIR } from "./fonts";

loadFonts();

const BG = "#0a0a0a";
const CREAM = "#e8e0d0";
const GOLD = "#c49a2a";
const WARM = "#c8a97a";

const GrainOverlay: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", opacity: 0.18, zIndex: 10 }}>
    <svg width="100%" height="100%">
      <filter id="grain">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.65"
          numOctaves="3"
          stitchTiles="stitch"
        />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#grain)" />
    </svg>
  </AbsoluteFill>
);

const DividerLine: React.FC = () => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [0, 40], ["0%", "60%"], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return (
    <div style={{ width, height: 1, background: GOLD, margin: "0 auto" }} />
  );
};

const ServiceItem: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const translateY = interpolate(frame, [0, 30], [16, 0], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return (
    <Interactive.Div
      name={`Service: ${text}`}
      style={{
        opacity,
        translate: `0px ${translateY}px`,
        fontFamily: `${ASSISTANT}, sans-serif`,
        fontSize: 38,
        color: CREAM,
        fontWeight: 300,
        letterSpacing: "0.08em",
        textAlign: "center",
        direction: "rtl",
        paddingBottom: 8,
      }}
    >
      {text}
    </Interactive.Div>
  );
};

export const IlanLeviIntro: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  const accentHeight = interpolate(frame, [10, 60], ["0%", "30%"], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const titleOpacity = interpolate(frame, [30, 80], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const titleY = interpolate(frame, [30, 80], [40, 0], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const subtitleOpacity = interpolate(frame, [80, 120], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const contactOpacity = interpolate(frame, [240, 280], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const services = ["ביקור בבית", "שיחה וקפה", "טיול ביחד", "משחק שחמט"];

  return (
    <AbsoluteFill style={{ background: BG, opacity: bgOpacity }}>
      <GrainOverlay />

      {/* Gold accent bar */}
      <div
        style={{
          position: "absolute",
          right: 60,
          top: "35%",
          width: 2,
          height: accentHeight,
          background: GOLD,
          transform: "translateY(-50%)",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "0 80px",
          direction: "rtl",
        }}
      >
        {/* Name */}
        <Interactive.Div
          name="Main title"
          style={{
            opacity: titleOpacity,
            translate: `0px ${titleY}px`,
            fontFamily: `${FRANK_RUHL}, serif`,
            fontSize: 130,
            fontWeight: 900,
            color: GOLD,
            letterSpacing: "0.04em",
            lineHeight: 1.1,
            textAlign: "center",
          }}
        >
          אילן לוי
        </Interactive.Div>

        {/* Divider */}
        <div style={{ marginTop: 24, marginBottom: 24, width: "100%" }}>
          <Sequence name="Divider" from={90} layout="none">
            <DividerLine />
          </Sequence>
        </div>

        {/* Tagline */}
        <Interactive.Div
          name="Tagline"
          style={{
            opacity: subtitleOpacity,
            fontFamily: `${PLAYFAIR}, serif`,
            fontStyle: "italic",
            fontSize: 46,
            color: WARM,
            letterSpacing: "0.06em",
            textAlign: "center",
            marginBottom: 80,
          }}
        >
          ליווי אישי · קשר אנושי
        </Interactive.Div>

        {/* Services */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16, alignItems: "center" }}>
          {services.map((service, i) => (
            <Sequence key={service} name={`Service ${i + 1}`} from={140 + i * 22} layout="none">
              <ServiceItem text={service} />
            </Sequence>
          ))}
        </div>

        {/* Contact */}
        <Interactive.Div
          name="Phone"
          style={{
            opacity: contactOpacity,
            marginTop: 90,
            fontFamily: `${ASSISTANT}, sans-serif`,
            fontSize: 36,
            color: CREAM,
            letterSpacing: "0.12em",
            textAlign: "center",
            direction: "ltr",
          }}
        >
          050-000-0000
        </Interactive.Div>

        <Interactive.Div
          name="Location"
          style={{
            opacity: contactOpacity,
            marginTop: 12,
            fontFamily: `${ASSISTANT}, sans-serif`,
            fontSize: 30,
            color: GOLD,
            letterSpacing: "0.08em",
            textAlign: "center",
          }}
        >
          רמת השרון והסביבה
        </Interactive.Div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
