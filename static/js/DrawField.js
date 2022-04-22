import Contour from "./Contour.js";
export let cont =[]
export  class DrawField {
  constructor(name, field) {
    (this.name = name),
      (this.field = field),
      (this.context = field.getContext("2d")),
      (this.field.width = this.field.clientWidth),
      (this.field.height = this.field.clientHeight);
    (this.field.drawingXmin = 0),
      (this.field.drawingYmin = 0),
      (this.field.drawingXmax = 0),
      (this.field.drawingYmin = 0),
      (this.field.drawingXstep = 0),
      (this.field.drawingYstep = 0),
      (this.field.drawingWidth = 0),
      (this.field.drawingHeight = 0),
      (this.field.scaleX = 0),
      (this.field.scaleY = 0),
      (this.drawBool = false),
      (this.contourID = 0);
  }
  style(lineW, color) {
    this.context.lineWidth = lineW;
    this.context.strokeStyle = color;
  }
  get_working_area(delta = 35, xmn, ymn, xmx, ymx, xst) {
    this.field.drawingXmin = delta;
    this.field.drawingYmin = delta;
    this.field.drawingXmax = this.field.width - delta;
    this.field.drawingYmax = this.field.height - delta;
    this.field.drawingWidth = this.field.drawingXmax - this.field.drawingXmin;
    this.field.drawingHeight = this.field.drawingYmax - this.field.drawingYmin;

    //Координаты в у.е.
    this.field.Xstep = xst;
    this.field.Ystep = ((ymx - ymn) / (xmx - xmn)) * xst;
    this.field.scaleX = this.field.drawingWidth / (xmx - xmn);
    this.field.scaleY = this.field.drawingHeight / (ymx - ymn);

    this.field.drawingXstep = this.field.Xstep * this.field.scaleX;
    this.field.drawingYstep = this.field.Ystep * this.field.scaleY;
    this.field.drawingX0 =
      this.field.drawingXmin + Math.abs(xmn) * this.field.scaleX;
    this.field.drawingY0 =
      this.field.drawingYmax - Math.abs(ymn) * this.field.scaleY;
    this.lsk(this.field.drawingX0, this.field.drawingY0);
    this.grid();
    this.gridNaming();
  }
  scale_checker(length) {
    if (length > 10) {
      return 0;
    } else if (length > 1) {
      return 1;
    } else if (length > 0.1) {
      return 2;
    }
  }
  lsk(x0, y0) {
    this.style(1, "black");
    this.draw_line_by_defaul(
      this.field.drawingXmin,
      y0,
      this.field.drawingXmax,
      y0
    );
    this.draw_line_by_defaul(
      x0,
      this.field.drawingYmin,
      x0,
      this.field.drawingYmax
    );
  }
  grid() {
    for (
      let ix = this.field.drawingX0;
      ix <= this.field.width;
      ix += this.field.drawingXstep
    ) {
      this.style(0.5, "grey");
      this.draw_line_by_defaul(ix, 0, ix, this.field.height);
    }
    for (
      let ix = this.field.drawingX0;
      ix >= 0;
      ix -= this.field.drawingXstep
    ) {
      this.style(0.5, "grey");
      this.draw_line_by_defaul(ix, 0, ix, this.field.height);
    }

    for (
      let iy = this.field.drawingY0;
      iy <= this.field.height;
      iy += this.field.drawingYstep
    ) {
      this.style(0.5, "grey");
      this.draw_line_by_defaul(0, iy, this.field.width, iy);
    }
    for (
      let iy = this.field.drawingY0;
      iy >= 0;
      iy -= this.field.drawingYstep
    ) {
      this.style(0.5, "grey");
      this.draw_line_by_defaul(0, iy, this.field.width, iy);
    }
  }

  draw_line_by_defaul(x0, y0, x1, y1) {
    this.context.beginPath();
    this.context.moveTo(x0, y0);
    this.context.lineTo(x1, y1);
    this.context.stroke();
    // this.context.closePath()
  }
  text(str, x, y, param = "xy") {
    this.context.font = `${Math.round(this.field.drawingXstep / 3)}pt Arial`;
    if (param == "xy") {
      this.context.fillText(
        str,
        x - this.field.drawingXstep * 0.7,
        y + this.field.drawingYstep * 1.2
      );
    } else if (param == "x") {
      this.context.fillText(str, x, y + this.field.drawingYstep);
    } else if (param == "y") {
      this.context.fillText(str, x - this.field.drawingXstep * 0.7, y);
    }
    
  }
  gridNaming(scale = 2) {
    for (
      let ix = this.field.drawingX0;
      ix <= this.field.drawingXmax;
      ix += scale * this.field.drawingXstep
    ) {
      this.text(
        `${((ix - this.field.drawingX0) / this.field.scaleX).toFixed(
          this.scale_checker(this.field.drawingWidth / this.field.scaleX)
        )}`,
        ix,
        this.field.drawingY0,
        "x"
      );
      this.style(1, "blue");
      this.draw_line_by_defaul(
        ix,
        this.field.drawingY0 - 5,
        ix,
        this.field.drawingY0 + 5
      );
    }

    for (
      let ix = this.field.drawingX0;
      ix >= this.field.drawingXmin;
      ix -= scale * this.field.drawingXstep
    ) {
      this.text(
        `${((ix - this.field.drawingX0) / this.field.scaleX).toFixed(
          this.scale_checker(this.field.drawingWidth / this.field.scaleX)
        )}`,
        ix,
        this.field.drawingY0,
        "x"
      );
      this.style(1, "blue");
      this.draw_line_by_defaul(
        ix,
        this.field.drawingY0 - 5,
        ix,
        this.field.drawingY0 + 5
      );
    }
    for (
      let iy = this.field.drawingY0;
      iy <= this.field.drawingYmax;
      iy += scale * this.field.drawingYstep
    ) {
      this.text(
        `${((this.field.drawingY0 - iy) / this.field.scaleY).toFixed(
          this.scale_checker(this.field.drawingHeight / this.field.scaleY)
        )}`,
        this.field.drawingX0,
        iy,
        "y"
      );
      this.style(1, "blue");
      this.draw_line_by_defaul(
        this.field.drawingX0 - 5,
        iy,
        this.field.drawingX0 + 5,
        iy
      );
    }
    for (
      let iy = this.field.drawingY0;
      iy >= this.field.drawingYmin;
      iy -= scale * this.field.drawingYstep
    ) {
      this.text(
        `${((this.field.drawingY0 - iy) / this.field.scaleY).toFixed(
          this.scale_checker(this.field.drawingHeight / this.field.scaleY)
        )}`,
        this.field.drawingX0,
        iy,
        "y"
      );
      this.style(1, "blue");
      this.draw_line_by_defaul(
        this.field.drawingX0 - 5,
        iy,
        this.field.drawingX0 + 5,
        iy
      );
    }
  }

  mouse_on(event) {
    console.log("Щёлк!");
    this.drawBool = true;
    let x = event.pageX - this.field.offsetLeft;
    let y = event.pageY - this.field.offsetTop;
    cont[this.contourID] = new Contour(this.contourID);
    cont[this.contourID].arrCoords.push([
      (x - this.field.drawingX0) / this.field.scaleX,
      (this.field.drawingY0 - y) / this.field.scaleY,
    ]);
    cont[this.contourID].baseArrCoords.push([x, y]);
    //рисую
    this.context.beginPath();
    this.context.moveTo(x, y);
  }
  mouse_move(event) {
    if (this.drawBool === true) {
      let x = event.pageX - this.field.offsetLeft;
      let y = event.pageY - this.field.offsetTop;
      cont[this.contourID].baseArrCoords.push([x, y]);
      cont[this.contourID].arrCoords.push([
        (x - this.field.drawingX0) / this.field.scaleX,
        (this.field.drawingY0 - y) / this.field.scaleY,
      ]);
      //рисую
      this.style(0.5, "red");
      this.context.lineTo(x, y);
      this.context.stroke();
    }
  }
  mouse_up(event) {
    let x = event.pageX - this.field.offsetLeft;
    let y = event.pageY - this.field.offsetTop;
    cont[this.contourID].baseArrCoords.push([x, y]);
    cont[this.contourID].arrCoords.push([
      (x - this.field.drawingX0) / this.field.scaleX,
      (this.field.drawingY0 - y) / this.field.scaleY,
    ]);
    //рисую
    this.context.lineTo(x, y);
    this.context.stroke();
    this.context.closePath();

    console.log(cont[this.contourID]);

    this.drawBool = false;
    this.contourID += 1;
  }
  aproximate(type){
     let x = [];
     let y = [];
     for (let j = 0; j < cont[this.contourID - 1].baseArrCoords.length; j++) {
       x.push(cont[this.contourID - 1].baseArrCoords[j][0]);
       y.push(cont[this.contourID - 1].baseArrCoords[j][1]);
     }
   
    let Niter = 200;
    let aa = 0;
    let bb = 0;
    let lmd1 =0.00000002
    let lmd2 = 0.000001
    console.log("x=", x);
    console.log('y=', y)
    //Функция ошибок:
    function E(x, y, a, b) {
      let ff = x.map((el) => a * el + b);
      let sum=0
      for (let k=0; k<y.length;k++){
          sum+=(y[k]-ff[k])**2
      }
      return sum
    }
    //Частная производная по а:
    function dEda(x, y, a, b) {
    let ff = x.map((el) => a * el + b);
    let sum = 0;
    for (let k = 0; k < y.length; k++) {
      sum += (y[k] - ff[k]) *ff[k];
    }
    return -2*sum;
    }
    //частная производная по б:
    function dEdb(x, y, a, b) {
    let ff = x.map((el) => a * el + b);
    let sum = 0;
    for (let k = 0; k < y.length; k++) {
      sum += (y[k] - ff[k]);
    }
    return -2 * sum;

    }
    //Градиентный спуск для двух параметров(линейная функция)
    for(let n=0; n<Niter; n++){
        aa = aa-lmd1*dEda(x, y, aa, bb)
        bb = bb - lmd2 * dEdb(x, y, aa, bb);
        console.log(`aa=${aa}, bb=${bb}`);
    }
    this.style(1, 'blue')
    this.draw_line_by_defaul(
      x[0],
      aa * x[0] + bb,
      x[x.length - 1],
      aa * x[x.length - 1] + bb
    );
    this.context.fillText(`y = ${aa}*x + ${bb}`, 300, 25);

  }
}
