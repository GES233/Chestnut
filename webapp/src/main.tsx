import app, { View, Update } from 'apprun';

type State = number;
const state: State = 0;

const Header = (content) => {
return (
<div> {/* Comment for JSX. */}
  <h1 class="bg-tiny-chestnut bg-opacity-75 text-4xl text-tiny-light-sec text-center font-semibold rounded">{content["content"]}</h1>
  <hr></hr>
</div>
)};

const view: View<State> = (state: State) => {
return (
<div class="text-center bg-tiny-dark-sec"><Header content="TinyUI build with Sanic and AppRun"/>
  <p class="font-mono text-center text-tiny-light-sec">Counter: <span class="text-2xl">{state}</span></p>
  <button class="bg-transparent border border-tiny-side-fir hover:bg-tiny-side-sec bg-opacity-50 rounded-full text-tiny-side-ter font-mono text-xl py-2 px-1" onclick={() => app.run("inc")}>+1</button>
  <button class="bg-transparent border border-tiny-side-fir hover:bg-tiny-side-sec bg-opacity-50 rounded-full text-tiny-side-ter font-mono text-xl py-2 px-1" onclick={() => app.run("dec")}>-1</button>
</div>
)};

const update: Update<State> = {
  "inc": (state) => state + 1,
  "dec": (state) => state - 1,
};

app.start("chestnut", state, view, update, {history: true});
