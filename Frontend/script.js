let navbar = document.querySelector(".header .navbar");
let uploadForm = document.querySelector(".imageInput .upload");
let result = document.querySelector(".imageInput .result");
let fileInputField = document.querySelector(".imageInput .upload .inputFile");
let uploadedImg = document.querySelector(".imageInput .uploadedImage");
const url = "http://127.0.0.1:5000/predict";

window.onscroll = () => {
  navbar.classList.remove("active");
};

async function getResponse(file) {
  var data = new FormData();
  data.append("file", file);

  const response = await fetch(url, {
    method: "POST",
    body: data,
  }).then((res) => res.json());

  return response;
}

async function predict() {
  return await getResponse(fileInputField.files[0])
    .catch(() => {
      alert("Server Error");
    })
    .then((response) => response);
}

function setResult(prediction) {
  console.log(prediction);
  var data;

  if (prediction.data) {
    data = `
      <div class="tg-wrap">
        <div class="table-top" style="text-align: center">
          Predicted Name: ${prediction.Name}
          <br />
          Calories (per 100gm): ${prediction.data.nutritions.calories}
        </div>
        <table class="tg">
          <thead>
            <tr>
              <th class="tg-rz9m" colspan="2">Nutritions (per 100gm)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="tg-hmp3">Carbohydrates</td>
              <td class="tg-hmp3" style="text-align:center">${prediction.data.nutritions.carbohydrates}</td>
            </tr>
            <tr>
              <td class="tg-0lax">Fat</td>
              <td class="tg-lqy6" style="text-align:center">${prediction.data.nutritions.fat}</td>
            </tr>
            <tr>
              <td class="tg-hmp3">Protein</td>
              <td class="tg-mb3i" style="text-align:center">${prediction.data.nutritions.protein}</td>
            </tr>
            <tr>
              <td class="tg-0lax">Sugar</td>
              <td class="tg-lqy6" style="text-align:center">${prediction.data.nutritions.sugar}</td>
            </tr>
          </tbody>
        </table>
      </div>`;
  } else {
    data = `
    <div class="tg-wrap">
      <div class="table-top">
        Predicted Name: ${prediction.Name}
      </div> 
      <div class="table-top" style="color:#f00">
        Cannot get nutrition data
      </div>
    </div>`
  }

  result.innerHTML = data;
  result.style.display = "flex";
}

async function showResult(event) {
  event.preventDefault();
  if (fileInputField.files[0]) {
    const prediction = await predict();
    setResult(prediction);
  } else {
    alert("Please select file");
  }
}

function showPreview() {
  if (fileInputField.files[0]) {
    imageURL = URL.createObjectURL(fileInputField.files[0]);
    uploadedImg.src = imageURL;
    uploadedImg.style.display = "initial";
  } else {
    uploadedImg.src = "";
    uploadedImg.style.display = "none";
    result.style.display = "none";
  }
}

uploadForm.addEventListener("submit", showResult);
fileInputField.addEventListener("change", showPreview);
