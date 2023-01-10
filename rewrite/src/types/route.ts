import { Request, Response } from "express";

type Mode = "get" | "post";

export default interface Route {
    route: string
    mode: Mode
    callback: (req: Request, res: Response) => Promise<void>
}