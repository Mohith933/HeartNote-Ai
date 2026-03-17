const CACHE_NAME = "heartnote-v1";
const STATIC_ASSETS = ["/", "/dashboard/", "/aiwrite/", "/static/pwa/manifest.json"];
self.addEventListener("install", event => {
    event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS)));
});
self.addEventListener("fetch", event => { if (!event.request.url.includes("/api/")) { event.respondWith(caches.match(event.request).then(res => res || fetch(event.request))); } });