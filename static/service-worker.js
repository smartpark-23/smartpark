self.addEventListener("install", (e) => {
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  caches.keys().then((names) => {
    for (let name of names) caches.delete(name);
  });
});