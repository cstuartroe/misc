const request = require('request');
const fs      = require('fs');
const cheerio = require('cheerio');

const localeFile = 'public/locales.json';
const emptyLocalesJSON = {
  completed: true,
  locales: {}
};
const wikiprefixes = ['https://en.wikipedia.org/wiki/', '/wiki/'];

function scrapeWikipedia(articleTitle) {
  const url = "https://en.wikipedia.org/wiki/" + articleTitle;
  request.get(url, function(err, response, body) {
    if (err) { return; }

    const $ = cheerio.load(body);

    var coords = $('span.geo-dec');
    if (coords.length == 0) { return; }
    var localeData = parseCoords(coords.first().text());

    localeData['name'] = $('title').text();
    localeData['name'] = localeData['name'].substring(0, localeData['name'].length - 12); // remove " - Wikipedia"

    var tables = $('table'), foundClimateTable = false;
    tables.each((i, table) => {
      var theader = $('th', table).first().text();
      if (!foundClimateTable &&
          theader.toLowerCase().includes('climate data')) {
        foundClimateTable = true;
        localeData = {
          ...localeData,
          ...parseClimateTable($, table)
        }
      }
    });

    if (foundClimateTable) {
      recordLocale(articleTitle, localeData);
    }

    $('a').each((i, link) => {
      var href = link.attribs.href;
      if (href) {
        wikiprefixes.map((prefix) => {
          if (href.startsWith(prefix)) {
            scrapeWikipedia(href.substring(prefix.length));
          }
        });
      }
    });
  });
}

function parseCoords(coordString) {
  var result = {},
      longitudeMultiplier;

  var coords;

  try {
    if (coordString.includes('E')) {
      longitudeMultiplier = 1;
      coordString = coordString.replace(/°E/g,'');
    } else if (coordString.includes('W')) {
      longitudeMultiplier = -1;
      coordString = coordString.replace(/°W/g,'');
    } else {
      throw new Exception("No longitude");
    }

    if (coordString.includes('N')) {
      coords = coordString.split('°N ').map(n => n-0);
      result['latitude'] = -coords[0];
    } else if (coordString.includes('S')) {
      coords = coordString.split('°S ').map(n => n-0);
      result['latitude'] = coords[0];
    } else {
      throw new Exception("No latitude");
    }

    result['longitude'] = longitudeMultiplier*coords[1];
  } catch(error) {
    console.log(coordString);
    console.error(error);
    result = {
      latitude: 0,
      longitude: 0
    };
  }

  return result;
}

function parseClimateTable($, table) {
  var result = {};

  $('tr', table).each((i, row) => {
    var rowHeader = $('th', row).first().text();
    if (rowHeader.toLowerCase().includes('average high')) {
      var temps = [];
      $('td',row).each((i, elem) => {
        temps.push($(elem).text());
      });
      var firstTemps = splitTemps(temps[0]);
      var celciusIndex = (firstTemps[1] > firstTemps[0]) ? 0 : 1;
      var tempsCelcius = temps.map((temp) => (
        splitTemps(temp)[celciusIndex]
      ));
      result["max_avg_high"] = Math.max(...tempsCelcius);
      result["min_avg_high"] = Math.min(...tempsCelcius);
    }
  });
  return result;
}

// converts, eg, "55(13)" to [55, 13]
function splitTemps(temps) {
  return temps.replace(/\)\n/g, '').split('(').map(n => n-0);
}

function recordLocale(articleTitle, localeData) {
  console.log(localeData);
  if (fs.existsSync(localeFile)) {
    fs.readFile(localeFile, 'utf8', function(err, contents) {
      writeLocale(articleTitle, localeData, JSON.parse(contents));
    });
  } else {
    writeLocale(articleTitle, localeData, emptyLocalesJSON);
  }
}

function writeLocale(articleTitle, localeData, localesJSON) {
  localesJSON.locales[articleTitle] = localeData;
  fs.writeFile(localeFile, JSON.stringify(localesJSON, null, 2), (err) => {
    if (err) { console.error(err); }
  });
}

scrapeWikipedia("San_Mateo,_California");
