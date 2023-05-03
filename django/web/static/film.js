// Get stars
const one = document.getElementById("1");
const two = document.getElementById("2");
const three = document.getElementById("3");
const four = document.getElementById("4");
const five = document.getElementById("5");

const form = document.getElementById("rate-form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const arr = [one, two, three, four, five];

const handle_select = (target_id) => {
  const target = parseInt(target_id);
  console.log(target)
  for (let i = 0; i < arr.length; i++) {
    if (i < target) {
      arr[i].classList.add("checked");
    } else {
      arr[i].classList.remove("checked");
    }
  }
};

arr.forEach((item) =>
  item.addEventListener("mouseover", (event) => handle_select(event.target.id))
);

arr.forEach((item) =>
  item.addEventListener("click", (event) => {
    console.log("clicked");
  })
);
