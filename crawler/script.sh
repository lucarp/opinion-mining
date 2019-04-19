

const axios = require('axios');
var fs = require('fs');
const path = require('path');

base_url = "https://api.twitter.com/1.1/search/tweets.json";

//#next_results = '?q=abortion&result_type=recent&count=100&lang=en';
//# continue from 1555598373746.json 
next_results = "?max_id=1116781854865051647&q=abortion&lang=en&count=100&include_entities=1&result_type=recent";

count = 0;

function downloadTweets() {
    axios.get(base_url + next_results + '&tweet_mode=extended', { headers: { Authorization: "Bearer AAAAAAAAAAAAAAAAAAAAAEjJagAAAAAA0UzkV1bBRIw43tlOy2kcxD1gwjI%3DckBntGor8t9SaInHwnyXqpGgciUzJ7f8FFQFNO1tDszU0p6Ds6" } })
    .then(response => {
        count++;
        console.log('Trying to download package',count); 

        var date = new Date();
        fs.writeFile("downloads/" + date.getTime() + '.json', JSON.stringify(response.data), 'utf8', function() {
            next_results = response.data.search_metadata.next_results;
            console.log('Downloaded',response.data.search_metadata.count,'tweets.'); 
            //setTimeout(function(){ downloadTweets(); }, 3000);
    	    downloadTweets();
        });
    })
    .catch(error => {
        console.log(error);
        //processDownload();
        setTimeout(function(){ downloadTweets(); }, 15 * 60 * 1000);
    });
}


downloadTweets();
/*processDownload();

function processDownload() {
    const directoryPath = path.join(__dirname, 'downloads');
    fs.readdir(directoryPath, function (err, files) {
        //handling error
        if (err) {
            return console.log('Unable to scan directory: ' + err);
        } 

        var statuses = []
        //listing all files using forEach
        files.forEach(function (file) {
            // Do whatever you want to do with the file
            var content = fs.readFileSync('downloads/'+file);
            content = JSON.parse(content);
            console.log(file,content.statuses.length);
            statuses = statuses.concat(content.statuses)

            fs.unlink(path.join(directoryPath, file), err => {
                if (err) throw err;
            });
        });
        
        var date = new Date();
        fs.writeFile('dataset/' + date.getTime(), JSON.stringify(statuses), function (err) {
            if (err) throw err;
            console.log('Merged!');
        });
    });
}
*/
