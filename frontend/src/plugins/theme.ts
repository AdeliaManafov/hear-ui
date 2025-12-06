// src/plugins/theme.ts
import type {ThemeDefinition} from 'vuetify';

/**
 * @description
 * This file defines the Vuetify theme for the application.
 * It includes color palettes and typography settings.
 *
 * Vuetify's theming system allows you to define a set of colors that will be applied
 * consistently across your application's components.
 *
 * For more information on Vuetify theming, visit:
 * https://vuetifyjs.com/en/features/theme/
 */

// Define a custom light theme. You can also create a 'darkTheme' and export it.
export const lightTheme: ThemeDefinition = {
    dark: false,
    colors: {
        white: '#FFFFFF',
        black: '#000000',
        primary: '#2196F3',
        secondary: '#424242',
        accent: '#A78BFA',
        error: '#FF5252',
        info: '#1976D2',
        success: '#4CAF50',
        warning: '#FB8C00',
        background: '#FFFFFF',
        surface: '#FFFFFF',
        logo_red: '#DD054A',
    },
    // Vuetify automatically provides typographic CSS classes (e.g., `text-h1`, `text-body-1`).
    // While you can override the SASS variables to change their default styles,
    // the recommended approach is to use these classes directly in your components.
    //
    // Example:
    // <h1 class="text-h1">Page Title</h1>
    // <p class="text-body-1">This is a paragraph of body text.</p>
    //
    // For global overrides of HTML tags like h1, h2, etc., you can add a separate
    // CSS file (e.g., `src/styles/typography.css`) and import it in `main.ts`.
};
