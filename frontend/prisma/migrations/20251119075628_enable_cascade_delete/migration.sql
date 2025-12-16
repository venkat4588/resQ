-- DropForeignKey
ALTER TABLE "public"."incidents" DROP CONSTRAINT "incidents_cctvId_fkey";

-- AddForeignKey
ALTER TABLE "incidents" ADD CONSTRAINT "incidents_cctvId_fkey" FOREIGN KEY ("cctvId") REFERENCES "cctvs"("id") ON DELETE CASCADE ON UPDATE CASCADE;
