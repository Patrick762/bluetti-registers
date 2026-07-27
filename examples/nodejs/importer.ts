import fs from "fs";
import { compile, JSONSchema } from "json-schema-to-typescript";

const tag = "0.0.8";

const url = `https://github.com/Patrick762/bluetti-registers/releases/download/${tag}/full.json`
const schema = `https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/tags/${tag}/schemas/all-devices.json`;
const enums = `https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/tags/${tag}/schemas/enums.json`;

const output = "devices.ts";

function compileEnums(schema: JSONSchema): string {
    const all = schema["anyOf"];

    if (!all) {
        return "";
    }

    let result = "";

    for (const e of all) {
        if (!e.title || !e.enum) {
            continue;
        }

        const name = e.title.trim().replaceAll(" ", "");

        result += `enum ${name} {`;

        for (let i = 0; i < e.enum.length; i++) {
            const n = e.enum[i];

            if (typeof n !== "string" || !isNaN(parseInt(n))) {
                continue;
            }

            result += `\n    ${n.toUpperCase()} = ${i},`;
        }

        result += "\n};\n\n";
    }

    return result;
}

async function importDevices() {
    const data = await fetch(url);
    const json = await data.json();

    const ds = await fetch(schema);
    const jsonschema = await ds.json();

    const de = await fetch(enums);
    const jsonschemae = await de.json();

    const s = await compile(jsonschema as JSONSchema, "DeviceList", { bannerComment: "// Generated File! DO NOT EDIT! Instead, run 'npm run import'" });
    const e = compileEnums(jsonschemae as JSONSchema);

    const content = `${s}\n${e}\n\nexport const DEVICES: DeviceSchema[] = ${JSON.stringify(json, null, 4)};\n`;

    fs.writeFileSync(output, content);
}

importDevices();
