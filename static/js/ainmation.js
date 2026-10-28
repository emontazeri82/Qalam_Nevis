// Shared Motion animations for Publish Desk.
const reducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
);

const activeAnimations = new Set();

let motion;
let stopObserving;
let generation = 0;

function stopAnimations() {
  generation += 1;

  stopObserving?.();
  stopObserving = undefined;

  for (const animation of activeAnimations) {
    animation.cancel();
  }

  activeAnimations.clear();
}

async function startAnimations() {
  stopAnimations();

  if (reducedMotion.matches) return;

  const currentGeneration = generation;

  const elements = [
    ...document.querySelectorAll("main [data-reveal]")
  ];

  if (!elements.length) return;

  try {
    motion ??= await import(
      "https://cdn.jsdelivr.net/npm/motion@12/+esm"
    );

    // Ignore a stale import if navigation or preferences changed.
    if (
      currentGeneration !== generation ||
      reducedMotion.matches
    ) {
      return;
    }

    stopObserving = motion.inView(
      elements,
      (element) => {
        if (reducedMotion.matches) return;

        const animation = motion.animate(
          element,
          {
            opacity: [0.8, 1],
            y: [12, 0]
          },
          {
            duration: 0.55,
            ease: [0.22, 1, 0.36, 1]
          }
        );

        activeAnimations.add(animation);

        const release = () => {
          activeAnimations.delete(animation);
        };

        animation.then(release, release);
      },
      {
        amount: 0.1
      }
    );
  } catch (error) {
    // Content is visible even when Motion cannot load.
    console.info("Animations unavailable; displaying the page normally.");
  }
}

reducedMotion.addEventListener("change", startAnimations);

window.addEventListener("pagehide", stopAnimations);

// Restart observation when returning through browser history.
window.addEventListener("pageshow", (event) => {
  if (event.persisted) startAnimations();
});

startAnimations();