import path from 'node:path'
import fsExtra from 'fs-extra'
import dotenv from 'dotenv'

const cwd = process.cwd()
const copy = fsExtra?.copy
const remove = fsExtra?.remove
const existsSync = fsExtra?.existsSync
const readdirSync = fsExtra?.readdirSync

dotenv.config()
dotenv.config({ path: `.env.${process.env.NODE_ENV}` })

// SSR状态
const isSSR = Boolean(process.env.NUXT_SSR)

// 目标的路径
const targetRelativePath = '../server/public/pc'

// 目标根路径
const releasePath = path.resolve(cwd, targetRelativePath)

// 发布的地图
const releaseMap = isSSR
    ? ['.output', 'static', 'package.json', '.env', '.env.production'].reduce(
        (prev, item) => {
            prev[item] = item
            return prev
        },
        {}
    )
    : ['.output/public'].reduce((prev, item) => {
        const readDir = readdirSync(item)
        for (const dir of readDir) {
            prev[path.join(item, dir)] = dir
        }
        return prev
    }, {})

// 打包方法
async function build() {
    // eslint-disable-next-line no-console
    console.log(`文件正在复制 ==> ${targetRelativePath}`)
    try {
        const allTask = Object.keys(releaseMap).map(async (key) => {
            const srcPath = path.resolve(cwd, key)
            const destPath = path.resolve(releasePath, releaseMap[key])
            if (existsSync(srcPath)) {
                if (existsSync(destPath)) {
                    await remove(destPath)
                }
                await copyFile(srcPath, destPath)
            }
        })
        await Promise.all(allTask)
    } catch (error) {
        // eslint-disable-next-line no-console
        console.log(`\n ${error}`)
    }
    // eslint-disable-next-line no-console
    console.log(`文件复制成功 ==> ${targetRelativePath}`)
}

// 拷贝方法
function copyFile(sourceDir, targetDir) {
    return new Promise((resolve, reject) => {
        copy(sourceDir, targetDir, { overwrite: true }, (err) => {
            if (err) {
                reject(err)
            } else {
                resolve()
            }
        })
    })
}

build().then(() => {})
