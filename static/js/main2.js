
import Contour from './Contour.js';
import { DrawField, cont} from './DrawField.js';


let canvas = document.querySelector("#canva");
if (canvas){
let df = new DrawField("iii", canvas);
df.field.addEventListener("mousedown", (e) => df.mouse_on(e));
df.field.addEventListener("mousemove", (e) => df.mouse_move(e));
df.field.addEventListener("mouseup", (e) => df.mouse_up(e));

let btnAddLsk = document.querySelector("#addLsk");

btnAddLsk.addEventListener("click", (e) => {
  let xmin = document.querySelector("#xmin").value;
  let xmax = document.querySelector("#xmax").value;
  let ymin = document.querySelector("#ymin").value;
  let ymax = document.querySelector("#ymax").value;
  let step = document.querySelector("#step").value;
  df.get_working_area(35, xmin, ymin, xmax, ymax, step);
   document.querySelector("#saveIntoFile").addEventListener("click", (e) => {
     e.preventDefault();
     dataJSON(cont[df.contourID - 1].id, cont[df.contourID - 1].arrCoords);
   });
   document.querySelector('#aproximate').addEventListener('click', e=>{
     e.preventDefault()
     df.aproximate()
   })
});
}



// function clientSide() {
async function dataJSON(id, arrCoords) {
    const res = await fetch("/pushCoords", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: id,
        coords: arrCoords,
      }),
    });
    if (res.ok === true) {
      console.log("aaaa");
    }
  };
// }



