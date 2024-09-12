import dotenv from 'dotenv'

dotenv.config({ path: `.env.${process.env.NODE_ENV}` })

const ENV_PREFIX: string = 'NUXT_'
export const getEnvConfig = () => {
    const config: Record<string, any> = {}
    Object.keys(process.env).forEach((evnKey: string): void => {
        if (evnKey.includes(ENV_PREFIX)) {
            const key: string = evnKey
                .replace(ENV_PREFIX, '')
                .toLowerCase()
                .replace(/_([A-Za-z])/g, function (_: string, $1) {
                    return $1.toUpperCase()
                })
            config[key] = process.env[evnKey]
        }
    })
    return config
}
