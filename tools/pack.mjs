// Compila src/packs/<nome>/*.json em LevelDB packs/<nome> com o CLI oficial do Foundry.
import { compilePack } from '@foundryvtt/foundryvtt-cli';
import { readdirSync, rmSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const SRC = 'src/packs';
const OUT = 'packs';
for (const name of readdirSync(SRC)) {
  const dest = join(OUT, name);
  if (existsSync(dest)) rmSync(dest, { recursive: true, force: true });
  await compilePack(join(SRC, name), dest, { log: false, recursive: false });
  console.log(`packed ${name}`);
}
