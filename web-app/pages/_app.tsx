import { DM_Sans } from 'next/font/google'
import '../styles/globals.css'
import type { AppProps } from 'next/app'

const dmSans = DM_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  display: 'swap',
})

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className={dmSans.className}>
      <Component {...pageProps} />
    </div>
  )
}
