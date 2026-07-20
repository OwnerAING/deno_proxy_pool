// main.ts
import { serve } from "https://deno.land/std/http/server.ts";

serve(async (req) => {
  // 这里替换成你的目标URL
  const targetUrl = "https://httpbin.org/ip";
  
  // 直接请求目标并返回结果，就这么简单
  return fetch(targetUrl);
});
