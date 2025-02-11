export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
    // Example authentication logic
    const token = req.headers.authorization;
    if (token) {
      // Validate token
      next();
    } else {
      res.status(401).send('Unauthorized');
    }
  };