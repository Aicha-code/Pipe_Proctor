# PipeProctor Frontend

PipeProctor Frontend is the React and Vite client for the PipeProctor project. It uses Tailwind CSS for styling, React Router for navigation, and Recharts for data visualization (charts).

## Dependencies
- React 19
- React DOM 19
- Vite 8
- Tailwind CSS 4
- React Router 7
- Recharts 3
- IBM Plex Sans 5 (variable) and IBM Plex Mono 5 — self-hosted via Fontsource

## Design tokens

Both the brand palette and the typefaces are declared in the `@theme` block of
`src/index.css`, so they are available as ordinary Tailwind utilities.

**Accent color** — the green of the Niger flag (`#0DB02B`) sits at `brand-500`,
with a full `brand-50` to `brand-950` scale around it. Use `brand-700` or darker
behind white text; it is the lightest step that clears the WCAG AA 4.5:1
contrast ratio.

**Typography** — IBM Plex Sans is the UI face and applies to the whole app
through Tailwind's preflight, so no wrapper class is needed. IBM Plex Mono is
available as `font-mono` for coordinates, sensor IDs, and timestamps. The font
files are installed as npm packages and imported in `src/main.jsx`, meaning they
are bundled and served locally — there is no request to a font CDN at runtime.
The variable sans covers weights 100–700, so avoid `font-extrabold` and
`font-black`, which the browser would have to synthesize.

## Runbook

1. Clone the repository
```bash
git clone https://github.com/Aicha-code/.git
cd Pipe_Proctor/
```
2. Access the frontend folder
```bash
cd frontend
```
> **Note:** No environment variables are required for local development.


3. Install dependencies
```bash
npm install
```
4. Run the frontend in dev mode

```bash
npm run dev
```
You can also copy and paste these commands from the frontend folder:
```bash
cd frontend
npm install
npm run dev
```


# References
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vite.dev/guide/)
- [Tailwind Documentation](https://tailwindcss.com/docs/installation/using-vite)
- [React Router Documentation](https://reactrouter.com/home)
- [Recharts Documentation](https://recharts.org/en-US/api)
- [IBM Plex typeface](https://www.ibm.com/plex/)
- [Fontsource Documentation](https://fontsource.org/docs/getting-started/introduction)
