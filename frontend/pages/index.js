import NavBar from "../components/NavBar"
import EloTableSection from "../components/EloTableSection"
import GameCardSection from "../components/GameCardSection"

export default function Home() {
  return (
    <div className="container">
      <section className="mainContent">
        <NavBar />
        <EloTableSection />
      </section>
      <div className="fullWidthContainer offsetBg">
        <section className="mainContent--noMinHeight">
          <GameCardSection />
        </section>
      </div>
    </div>
  )
}
