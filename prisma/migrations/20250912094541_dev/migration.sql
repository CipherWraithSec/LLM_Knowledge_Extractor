-- CreateTable
CREATE TABLE "Analysis" (
    "id" SERIAL NOT NULL,
    "title" TEXT,
    "topics" TEXT[],
    "sentiment" TEXT NOT NULL,
    "keywords" TEXT[],
    "summary" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Analysis_pkey" PRIMARY KEY ("id")
);
