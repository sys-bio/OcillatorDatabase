let paths = [];

function lookup(species_num = null, model_type = null, reaction_num = null) {
  data = load_metadate();
  paths = data
    .filter(
      (item) =>
        (species_num === null || item.numSpecies === species_num) &&
        (reaction_num === null || item.numReactions === reaction_num) &&
        (model_type === null || item.modelType === model_type),
    )
    .map((item) => item.path);
  return paths.length;
}

function load_metadate() {
  fetch("metadata.json")
    .then((response) => response.json())
    .then((data) => {
      return data;
    });
}

async function fetchFile(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Network response was not ok ' + response.statusText);
  }
  return response.blob();
}

async function downloadFiles() {
  if (paths.length === 0) {
    return;
    //modify something!
  }
  const zip = new JSZip();
  for (const path of paths) {
    const filename = path.split('/').pop();
    const fileBlob = await fetchFile(path);
    zip.file(filename, fileBlob);
  }

  const content = await zip.generateAsync({type: 'blob'});
  saveAs(content, `${resultantDir}.zip`);
}