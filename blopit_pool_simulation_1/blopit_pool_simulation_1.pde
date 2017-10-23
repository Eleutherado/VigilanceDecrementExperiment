
void setup() {
  size(1200, 700);
  println(width);
}

int width = 1200; // must match parameters in 'size' function called in the setup(). Declaring them here for correct use in global space 
int height = 700; // must match parameters in 'size' function called in the setup(). Declaring them here for correct use in global space

int numSwimmers = 15;

int borderWidth = width/15;
int borderHeight = height/15;
int poolWidth = width - 2 * borderWidth;
int poolHeight = height - 2 * borderHeight;

int swimmerColOffset = poolWidth/(numSwimmers + 1);
int swimmerWidth = 25;
int swimmerHeight = 25;

void draw() {
   fill(225);
   rect(0, 0, width, height); 
   fill(87, 149, 249);
   rect(borderWidth, borderWidth, width - 2 * borderWidth, height - 2 * borderWidth);
   for(int i = 0; i < numSwimmers; i++)
     drawSwimmer(i + 1);
}

void drawSwimmer(int swimmer){
  fill(239, 219, 14);
  int swimX = borderWidth + swimmer * swimmerColOffset;
  int swimY = height/2;
  ellipse(swimX, swimY, swimmerWidth, swimmerHeight);
  noFill();
  //left eye
  ellipse(swimX - swimmerWidth/5, swimY - swimmerHeight/7, swimmerWidth/6, swimmerHeight/5);
  //right eye
  ellipse(swimX + swimmerWidth/5, swimY - swimmerHeight/7, swimmerWidth/6, swimmerHeight/5);
  
  arc(swimX, swimY + swimmerHeight/6, swimmerWidth/2, swimmerHeight/6, PI/10, PI);
  
}