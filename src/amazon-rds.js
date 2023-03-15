import jsdom from 'jsdom'
import axios from 'axios'
import fs from 'fs'

const { JSDOM } = jsdom

// writes a date in the iso format endoflife wants
function format(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`
}

const dbs = {
  'mysql': 'https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html',
  'postgresql': 'https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html',
}

for (const [db, url] of Object.entries(dbs)) {
  const html = await axios.get(url)
    .then(res => res.data)
    .catch(console.log)
  const dom = new JSDOM(html)
  
  // select all table tags
  const tables = dom.window.document.getElementsByTagName('table') 
  
  const releases = {}

  for (const [i, table] of Object.entries(tables)) {

    // first table is minor, second is major
    let minor = false
    if (i === '0') {
      console.log('AWS RDS: Scraping', db, 'minor')
      minor = true
    } else {
      console.log('AWS RDS: Scraping', db, 'major')
    }

    // select the table rows
    const rows = table.getElementsByTagName('tr')

    for (const row of rows) {
      // ignore rows which just contain a major version with no data
      if (row.childNodes.length === 3) continue
    
      let version = ''

      for (let [num, col] of row.childNodes.entries()) {
        // ignore all nodes that are not Table Data
        if (col.tagName !== 'TD') continue

        // for some reason postgresql iteration is off by one
        if (db === 'postgresql' && i === '1') {
          num++
        }

        if (num === 1) {
          const lines = col.textContent.trim().split('\n')
          version = lines[0].replace(/[^0-9.]/g, '')
        } else if (num === 7) {
          
          // minor tables do not have a Community end of life column
          // due to different table column size a conditional is necessary
          if (minor) {
            // RDS end of standard support date
            const date = format(new Date(col.textContent.trim()))
            // console.log('RDS end of standard support date', date)
            // release.eol = date
            // minors.push(release)
            releases[version] = date
          }

        } else if (num === 9) {
          // only major tables have this column
          // RDS end of standard support date
          const date = format(new Date(col.textContent.trim()))
          // console.log('RDS end of standard support date', date)
          // release.eol = date
          // majors.push(release)
          releases[version] = date
        }
      }
    }
  }

  fs.writeFileSync(`releases/amazon-rds-${db}.json`, JSON.stringify(releases, null, 2))
}