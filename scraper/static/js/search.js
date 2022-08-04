const searchField = document.querySelector('#searchField');

const output = document.querySelector('.output');
const scraperOutput = document.querySelector('.scraper-output');
output.style.display = 'none';
const body = document.querySelector('.inner-output');

searchField.addEventListener('keyup', (e)=>{

    const searchValue=e.target.value;

    if(searchValue.trim().length>0){
        body.innerHTML=''
        console.log('searchValue', searchValue)
    fetch("/search", {
        body: JSON.stringify({searchText: searchValue}),
        method: "POST",
    })
        .then((res) => res.json())
        .then((data) =>{
            console.log('data', data);
            scraperOutput.style.display = "none";
            output.style.display = "flex";
            if(data.length===0){
                body.innerHTML='No Results found';
            } else {
                data.forEach(item=>{
                body.innerHTML+=`
                        <div class="card" style="width: 25rem; margin: 10px;">
                            <img class="card-img-top" src="${item.content_image}" style="width: 90%">
                                <div class="card-body">
                                    <div style="display: flex; padding: 2px">
                                        <img src="${item.image}" style="width: 50px; height: 50px; margin-right: 5px">
                                            <h5 className="card-title">${item.title}</h5>
                                    </div>
                                    <p class="card-text text_reduction" id="${ item.id }">
                                        ${item.content_summary}
                                    </p>
                                    <div class="container">
                                        <div class="btn-holder">
                                            <a href="${item.content_link}" target="_blank"
                                               class="btn btn-primary">Go to Article</a>
                                        </div>
                                    </div>
                                </div>
                        </div>
                `
                })

            }
        });

    } else {
         scraperOutput.style.display = "flex";
         output.style.display = "none";
    }

})