// main.ts
import { serve } from "https://deno.land/std/http/server.ts";

serve(async (req) => {
  // 从请求参数中获取你要去访问的目标URL
  const url = new URL(req.url).searchParams.get("url");

  // 简单安全检查，防止滥用
  if (!url) {
    return new Response("Missing 'url' parameter", { status: 400 });
  }

  // 转发原始请求的头部信息（可选的，能帮你模拟得更像真实浏览器）
  const headers = new Headers(req.headers);
  headers.set("X-Forwarded-For", "hidden"); 

  // 向目标发起请求
  return fetch(url, {
    headers: headers,
    method: req.method,
    body: req.body,
  });
});
