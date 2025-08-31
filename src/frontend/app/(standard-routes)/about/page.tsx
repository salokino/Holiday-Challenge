
export default function AboutPage() {

  const classNamesHeading = "text-3xl font-bold text-sky-800 pt-12 pb-4 [font-variant:small-caps]"
  return (
    <div className="grid justify-center p-20">
      <div className="grid">
        <p className={classNamesHeading}>
          About the Challenge
        </p>
        <p>
          The name of the challenge, the <strong className="text-sky-800">Check24 TechUp Holiday Challenge</strong>, provides a good indication of what was expected.
        </p>
        <p>
          Participants were given access to over 100 million genuine offers for holidays to Mallorca and were tasked with creating a simple holiday portal
        </p>
        <p>
          to help users find trips to the island. Therefore, the participants had to solve two major problems:
        </p>
        <br />
        <ul className="list-disc pl-6">
          <li>
            Building a backend service that stores the data and allows for efficient querying.
          </li>
          <li>
            Building a front-end service that lets users search through the data.
          </li>
        </ul>
        <br />
        <p>
          More information is available at:{" "}
          <a
            href="https://github.com/TechUp-Stipendium/holiday-coding-challenge/tree/main"
            className="text-sky-800 hover:text-sky-900"
            target="_blank"
            rel="noopener noreferrer"
          >
            https://github.com/TechUp-Stipendium/holiday-coding-challenge/tree/main
          </a>
        </p>






      </div>
      <div className="grid">
        <p className={classNamesHeading}>
          About the Developer
        </p>
        <p>
          Hey there! I&apos;m <strong className="text-sky-800">Nikolas</strong>, a computer science student at the University of Leipzig.
        </p>
        <p>
          I will graduate this summer and am currently enjoying the time between submitting my bachelor&apos;s thesis
        </p>
        <p>
          and receiving the results. I heard about this interesting challenge and was hooked immediately.
        </p>
        <p>
          The project involves working with large amounts of data, creating a database and writing efficient queries.
        </p>
        <p>
          This is why I am going to pursue a Master&apos;s degree in Data Science in Leipzig, with the aim of becoming a data engineer or analyst.
        </p>
        <p>
          Thank you for reading these few lines.
        </p>
      </div>
    </div>
  )
}