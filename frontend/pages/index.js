import Head from "next/head"
import NavBar from "../components/NavBar"
import EloTableSection from "../components/EloTableSection"
import GameCardSection from "../components/GameCardSection"

export default function Home() {
  return (
    <div>
      <Head>
        <title>Hockey Elo</title>
        <meta property="og:title" content="Hockey Elo" key="title" />
        <meta name="description" content="Elo rankings for NHL teams" />
        <meta name="keywords" content="hockey, elo, rankings, sports" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
        <meta name="msapplication-TileColor" content="#da532c" />
        <meta name="theme-color" content="#ffffff" />
      </Head>
      <div className="container">
        <section className="mainContent">
          <NavBar />
          <EloTableSection />
        </section>
        <div className="fullWidthContainer offsetBg">
          <div className="mainContent--noMinHeight">
            <GameCardSection />
          </div>
        </div>
      </div>
    </div>
  )
}
