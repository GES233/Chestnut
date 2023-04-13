import app, { View, Update } from 'apprun';

type State = number;
const state: State = 0;


const view: View<State> = (state: State) => {
return (
<div class="text-center bg-tinyui-chestnut-leading">
  <p class="font-mono text-center bg-tinyui-chestnut-superleading">Counter: <span class="text-2xl">{state}</span></p>
  <button class="bg-transparent border border-tinyui-chestnut-submediant hover:bg-tinyui-chestnut-dominant bg-opacity-50 rounded-full text-bg-tinyui-chestnut-subdominant font-mono text-xl py-2 px-1" onclick={() => app.run("inc")}>+1</button>
  <button class="bg-transparent border border-tinyui-chestnut-submediant hover:bg-tinyui-chestnut-dominant bg-opacity-50 rounded-full text-tinyui-chestnut-subdominant font-mono text-xl py-2 px-1" onclick={() => app.run("dec")}>-1</button>
</div>
)};

const update: Update<State> = {
  "inc": (state) => state + 1,
  "dec": (state) => state - 1,
};

app.start("chestnut", state, view, update, {history: true});
