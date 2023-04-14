import app, { View, Update } from 'apprun';

type State = number;
const state: State = 0;


const view: View<State> = (state: State) => {
return (
<div class="bg-chestnut-ui-tonic">
  <h1 class="text-center">Chestnut</h1>
  <p class="font-mono text-center bg-chestnut-ui-superleading">Counter: <span class="text-2xl">{state}</span></p>
  <button class="bg-transparent border border-chestnut-ui-submediant hover:bg-chestnut-ui-dominant bg-opacity-50 rounded-full text-chestnut-ui-subdominant font-mono text-xl py-2 px-1" onclick={() => app.run("inc")}>+1</button>
  <button class="bg-transparent border border-chestnut-ui-submediant hover:bg-chestnut-ui-dominant bg-opacity-50 rounded-full text-chestnut-ui-subdominant font-mono text-xl py-2 px-1" onclick={() => app.run("dec")}>-1</button>
</div>
)};

const update: Update<State> = {
  "inc": (state) => state + 1,
  "dec": (state) => state - 1,
};

app.start("chestnut", state, view, update, {history: true});
