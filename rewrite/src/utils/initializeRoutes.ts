import { Express } from "express";

import routes from "../routes";

export default function initializeRoutes(app: Express) {
    for (let route of routes) {
        let success = true;

        switch (route.mode) {
            case "get":
                app.get(route.route, route.callback); break;
            case "post":
                app.post(route.route, route.callback); break;
            default:
                success = false;
                console.log(`[Route: ${route.route}] This route does not have a valid mode`);
                break;
        }

        if (success) {
            console.log(`[Route: ${route.route}] This route has initialized successfully`);
        }
    }
}