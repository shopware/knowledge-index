import {
    defineConfig,
    presetIcons,
    presetUno,
    transformerDirectives,
} from 'unocss'

export default defineConfig({
    // ...UnoCSS options
    presets: [
        presetUno(),
        presetIcons({
            scale: 1.2,
            warn: true,
        }),
    ],
    transformers: [
        transformerDirectives(),
    ]
})